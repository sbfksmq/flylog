# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flylog import Client


client = Client()


def main():
    client.send('test source', 'test content', )
    client.send('测试source', '测试content', )


if __name__ == '__main__':
    main()
