import struct, os, time
import zlib, io, _compression, builtins


def inflate(data: str):
    """A.K.A. compression"""
    data = data.encode("UTF-8")
    with process("temp_file.txt", "wb") as temp_file:
        temp_file.write(data)
    with open("temp_file.txt", "r", errors='ignore') as temp_file:
        result = temp_file.read()
    return result


def deflate(data):
    """A.K.A. decompression"""
    with process("temp_file.txt", 'rb') as temp_file:
        info = temp_file.read()
    os.remove("temp_file.txt")
    return info


def process(filename, mode="rb", compresslevel=9, encoding=None, errors=None, newline=None):
    if "t" in mode:
        if "b" in mode:
            raise ValueError("Invalid mode: %r" % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")

    gz_mode = mode.replace("t", "")
    if isinstance(filename, (str, bytes, os.PathLike)):
        binary_file = GzipFile(filename, gz_mode, compresslevel)
    elif hasattr(filename, "read") or hasattr(filename, "write"):
        binary_file = GzipFile(None, gz_mode, compresslevel, filename)
    else:
        raise TypeError("filename must be a str or bytes object, or a file")

    if "t" in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file


def write32u(output, value):
    output.write(struct.pack("<L", value))


class _PaddedFile:
    def __init__(self, f, prepend=b''):
        self._buffer = prepend
        self._length = len(prepend)
        self.file = f
        self._read = 0

    def read(self, size):
        if self._read is None:
            return self.file.read(size)
        if self._read + size <= self._length:
            read = self._read
            self._read += size
            return self._buffer[read:self._read]
        else:
            read = self._read
            self._read = None
            return self._buffer[read:] + \
                   self.file.read(size-self._length+read)

    def prepend(self, prepend=b''):
        if self._read is None:
            self._buffer = prepend
        else:  # Assume data was read since the last prepend() call
            self._read -= len(prepend)
            return
        self._length = len(self._buffer)
        self._read = 0

    def seek(self, off):
        self._read = None
        self._buffer = None
        return self.file.seek(off)

    def seekable(self):
        return True  # Allows fast-forwarding even in unseekable streams


class BadGzipFile(OSError):
    """Exception raised in some cases for invalid gzip files."""


class GzipFile(_compression.BaseStream):
    def __init__(self, filename=None, mode=None, compresslevel=9, fileobj=None, mtime=None):
        if mode and ('t' in mode or 'U' in mode):
            raise ValueError("Invalid mode: {!r}".format(mode))
        if mode and 'b' not in mode:
            mode += 'b'
        if fileobj is None:
            fileobj = self.myfileobj = builtins.open(filename, mode or 'rb')
        if filename is None:
            filename = getattr(fileobj, 'name', '')
            if not isinstance(filename, (str, bytes)):
                filename = ''
        else:
            filename = os.fspath(filename)
        if mode is None:
            mode = getattr(fileobj, 'mode', 'rb')

        if mode.startswith('r'):
            self.mode = 1
            raw = _GzipReader(fileobj)
            self._buffer = io.BufferedReader(raw)
            self.name = filename

        elif mode.startswith(('w', 'a', 'x')):
            self.mode = 2
            self._init_write(filename)
            self.compress = zlib.compressobj(compresslevel,
                                             zlib.DEFLATED,
                                             -zlib.MAX_WBITS,
                                             zlib.DEF_MEM_LEVEL,
                                             0)
            self._write_mtime = mtime
        else:
            raise ValueError("Invalid mode: {!r}".format(mode))

        self.fileobj = fileobj

        if self.mode == 2:
            self._write_gzip_header(compresslevel)

    @property
    def filename(self):
        import warnings
        warnings.warn("use the name attribute", DeprecationWarning, 2)
        if self.mode == 2 and self.name[-3:] != ".gz":
            return self.name + ".gz"
        return self.name

    @property
    def mtime(self):
        """Last modification time read from stream, or None"""
        return self._buffer.raw._last_mtime

    def __repr__(self):
        s = repr(self.fileobj)
        return '<gzip ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    def _init_write(self, filename):
        self.name = filename
        self.crc = zlib.crc32(b"")
        self.size = 0
        self.writebuf = []
        self.bufsize = 0
        self.offset = 0  # Current file offset for seek(), tell(), etc

    def _write_gzip_header(self, compresslevel):
        self.fileobj.write(b'\037\213')             # magic header
        self.fileobj.write(b'\010')                 # compression method
        try:
            # RFC 1952 requires the FNAME field to be Latin-1. Do not
            # include filenames that cannot be represented that way.
            fname = os.path.basename(self.name)
            if not isinstance(fname, bytes):
                fname = fname.encode('latin-1')
            if fname.endswith(b'.gz'):
                fname = fname[:-3]
        except UnicodeEncodeError:
            fname = b''
        flags = 0
        if fname:
            flags = 8
        self.fileobj.write(chr(flags).encode('latin-1'))
        mtime = self._write_mtime
        if mtime is None:
            mtime = time.time()
        write32u(self.fileobj, int(mtime))
        if compresslevel == 9:
            xfl = b'\002'
        elif compresslevel == 1:
            xfl = b'\004'
        else:
            xfl = b'\000'
        self.fileobj.write(xfl)
        self.fileobj.write(b'\377')
        if fname:
            self.fileobj.write(fname + b'\000')

    def write(self,data):
        self._check_not_closed()
        if self.mode != 2:
            import errno
            raise OSError(errno.EBADF, "write() on read-only GzipFile object")

        if self.fileobj is None:
            raise ValueError("write() on closed GzipFile object")

        if isinstance(data, bytes):
            length = len(data)
        else:
            # accept any data that supports the buffer protocol
            data = memoryview(data)
            length = data.nbytes

        if length > 0:
            self.fileobj.write(self.compress.compress(data))
            self.size += length
            self.crc = zlib.crc32(data, self.crc)
            self.offset += length

        return length

    def read(self, size=-1):
        self._check_not_closed()
        if self.mode != 1:
            import errno
            raise OSError(errno.EBADF, "read() on write-only GzipFile object")
        return self._buffer.read(size)

    def read1(self, size=-1):
        """Implements BufferedIOBase.read1()

        Reads up to a buffer's worth of data if size is negative."""
        self._check_not_closed()
        if self.mode != 1:
            import errno
            raise OSError(errno.EBADF, "read1() on write-only GzipFile object")

        if size < 0:
            size = io.DEFAULT_BUFFER_SIZE
        return self._buffer.read1(size)

    def peek(self, n):
        self._check_not_closed()
        if self.mode != 1:
            import errno
            raise OSError(errno.EBADF, "peek() on write-only GzipFile object")
        return self._buffer.peek(n)

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        fileobj = self.fileobj
        if fileobj is None:
            return
        self.fileobj = None
        try:
            if self.mode == 2:
                fileobj.write(self.compress.flush())
                write32u(fileobj, self.crc)
                # self.size may exceed 2 GiB, or even 4 GiB
                write32u(fileobj, self.size & 0xffffffff)
            elif self.mode == 1:
                self._buffer.close()
        finally:
            myfileobj = self.myfileobj
            if myfileobj:
                self.myfileobj = None
                myfileobj.close()

    def flush(self,zlib_mode=zlib.Z_SYNC_FLUSH):
        self._check_not_closed()
        if self.mode == 2:
            # Ensure the compressor's buffer is flushed
            self.fileobj.write(self.compress.flush(zlib_mode))
            self.fileobj.flush()

    def fileno(self):
        """Invoke the underlying file object's fileno() method.

        This will raise AttributeError if the underlying file object
        doesn't support fileno().
        """
        return self.fileobj.fileno()

    def rewind(self):
        '''Return the uncompressed stream file position indicator to the
        beginning of the file'''
        if self.mode != 1:
            raise OSError("Can't rewind in write mode")
        self._buffer.seek(0)

    def readable(self):
        return self.mode == 1

    def writable(self):
        return self.mode == 2

    def seekable(self):
        return True

    def seek(self, offset, whence=io.SEEK_SET):
        if self.mode == 2:
            if whence != io.SEEK_SET:
                if whence == io.SEEK_CUR:
                    offset = self.offset + offset
                else:
                    raise ValueError('Seek from end not supported')
            if offset < self.offset:
                raise OSError('Negative seek in write mode')
            count = offset - self.offset
            chunk = b'\0' * 1024
            for i in range(count // 1024):
                self.write(chunk)
            self.write(b'\0' * (count % 1024))
        elif self.mode == 1:
            self._check_not_closed()
            return self._buffer.seek(offset, whence)

        return self.offset

    def readline(self, size=-1):
        self._check_not_closed()
        return self._buffer.readline(size)


class _GzipReader(_compression.DecompressReader):
    def __init__(self, fp):
        super().__init__(_PaddedFile(fp), zlib.decompressobj,
                         wbits=-zlib.MAX_WBITS)
        # Set flag indicating start of a new member
        self._new_member = True
        self._last_mtime = None

    def _init_read(self):
        self._crc = zlib.crc32(b"")
        self._stream_size = 0  # Decompressed size of unconcatenated stream

    def _read_exact(self, n):
        data = self._fp.read(n)
        while len(data) < n:
            b = self._fp.read(n - len(data))
            if not b:
                raise EOFError("Compressed file ended before the "
                               "end-of-stream marker was reached")
            data += b
        return data

    def _read_gzip_header(self):
        magic = self._fp.read(2)
        if magic == b'':
            return False

        if magic != b'\037\213':
            raise BadGzipFile('Not a gzipped file (%r)' % magic)

        (method, flag,
         self._last_mtime) = struct.unpack("<BBIxx", self._read_exact(8))
        if method != 8:
            raise BadGzipFile('Unknown compression method')

        if flag & 4:
            # Read & discard the extra field, if present
            extra_len, = struct.unpack("<H", self._read_exact(2))
            self._read_exact(extra_len)
        if flag & 8:
            # Read and discard a null-terminated string containing the filename
            while True:
                s = self._fp.read(1)
                if not s or s==b'\000':
                    break
        if flag & 16:
            # Read and discard a null-terminated string containing a comment
            while True:
                s = self._fp.read(1)
                if not s or s==b'\000':
                    break
        if flag & 2:
            self._read_exact(2)     # Read & discard the 16-bit header CRC
        return True

    def read(self, size=-1):
        if size < 0:
            return self.readall()
        if not size:
            return b""
        while True:
            if self._decompressor.eof:
                self._read_eof()
                self._new_member = True
                self._decompressor = self._decomp_factory(
                    **self._decomp_args)

            if self._new_member:
                self._init_read()
                if not self._read_gzip_header():
                    self._size = self._pos
                    return b""
                self._new_member = False
            buf = self._fp.read(io.DEFAULT_BUFFER_SIZE)

            uncompress = self._decompressor.decompress(buf, size)
            if self._decompressor.unconsumed_tail != b"":
                self._fp.prepend(self._decompressor.unconsumed_tail)
            elif self._decompressor.unused_data != b"":
                self._fp.prepend(self._decompressor.unused_data)

            if uncompress != b"":
                break
            if buf == b"":
                raise EOFError("Compressed file ended before the "
                               "end-of-stream marker was reached")

        self._add_read_data( uncompress )
        self._pos += len(uncompress)
        return uncompress

    def _add_read_data(self, data):
        self._crc = zlib.crc32(data, self._crc)
        self._stream_size = self._stream_size + len(data)

    def _read_eof(self):
        crc32, isize = struct.unpack("<II", self._read_exact(8))
        if crc32 != self._crc:
            raise BadGzipFile("CRC check failed %s != %s" % (hex(crc32),
                                                             hex(self._crc)))
        elif isize != (self._stream_size & 0xffffffff):
            raise BadGzipFile("Incorrect length of data produced")
        c = b"\x00"
        while c == b"\x00":
            c = self._fp.read(1)
        if c:
            self._fp.prepend(c)

    def _rewind(self):
        super()._rewind()
        self._new_member = True
