# -*- coding: utf-8 -*-
import math
import os
import time
import asyncio
import aiofiles
from aiofile import AIOFile, Reader, LineReader


class BigFileCache:
    MAX_CACHE_FILE_LINE_COUNT = 10000
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024
    TB = GB * 1024
    SPLIT_FILE_SIZE = 100 * MB

    def __init__(self, file_path):
        self.__file_path = file_path
        asyncio.run(self.__create_cache_files())

    async def __quick_create_cache_files(self):
        # async with aiofiles.open(self.__file_path, "r") as fp:
        #     lines = await fp.readlines()
        with open(self.__file_path, "r") as fp:
            lines = fp.readlines()
            lines_len = len(lines)
            cache_files_count = int(math.ceil(lines_len / self.MAX_CACHE_FILE_LINE_COUNT))
            for index in range(0, cache_files_count):
                cache_data_begin = index * self.MAX_CACHE_FILE_LINE_COUNT
                cache_data_end = cache_data_begin + self.MAX_CACHE_FILE_LINE_COUNT
                if cache_data_end > lines_len:
                    cache_data_end = lines_len
                cache_file_name = "{}_{}.cache".format(
                    self.__file_path,
                    cache_data_end
                )
                await self.__new_cache_file(cache_file_name,lines[cache_data_begin:cache_data_end])

    @staticmethod
    async def __new_cache_file(file_path: str, cache_data: list):
        # async with AIOFile(file_path, "w") as afp:
        #     [afp.write(x) for x in cache_data]
        # with open(file_path, "w") as fp:
        #     fp.writelines(cache_data)
        async with aiofiles.open(file_path, "w") as fp:
            fp.writelines(cache_data)

    async def __create_cache_files(self):
        if not self.__file_path:
            return None
        file_size = os.path.getsize(self.__file_path)
        if file_size <= self.SPLIT_FILE_SIZE:
            return await self.__quick_create_cache_files()
        async with AIOFile(self.__file_path, "r") as afp:
            print(afp.fileno())
            async for line in LineReader(afp):
                print(line)


if __name__ == '__main__':
    begin_time = time.time()
    # file = BigFileCache("../../tests/big_file.log")
    file = BigFileCache("../../tests/trace_log_1.log")
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(write_file_demo())
    end_time = time.time()
    print("start:{} end:{} {}".format(
        begin_time, end_time, (end_time - begin_time) / 1000
    ))
