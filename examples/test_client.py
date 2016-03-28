# -*- coding: utf-8 -*-


from flylog import Client


client = Client()


def main():
    client.send('test source', 'test content', )


if __name__ == '__main__':
    main()
