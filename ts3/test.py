import unittest
from ts3 import TS3Proto

class TS3ProtoTest(unittest.TestCase):
    """ Tests the TS3Proto class """

    def setUp(self):

        self.ts3 = TS3Proto()

    def testCharacterEscaping(self):

        teststr = b'|/ abcdefg| |'
        expected = str.encode(r'\p\/\sabcdefg\p\s\p')

        res = self.ts3._escape_str(teststr)
        self.assertEqual(res, expected)

    def testControlEscaping(self):

        teststr = b"\n\r\t"
        expected = str.encode(r'\n\r\t')

        self.assertEqual(self.ts3._escape_str(teststr), expected)

    def testCharacterUnEscaping(self):

        teststr = str.encode(r'\p\/\sabcdefg\p\s\p')
        expected = b'|/ abcdefg| |'

        self.assertEqual(self.ts3._unescape_str(teststr), expected)

    def testFullCircle(self):

        teststr = b'|/ abcdefg| |'
        res = self.ts3._unescape_str(self.ts3._escape_str(teststr))

        self.assertEqual(res, teststr)

    def testConstructBasic(self):
        self.assertEqual(self.ts3.construct_command('testcommand'), 'testcommand')
        self.assertEqual(self.ts3.construct_command('testcommand', opts=['test']), 'testcommand -test')
        self.assertEqual(self.ts3.construct_command('testcommand', opts=['test1', 'test2', 'test3']), 'testcommand -test1 -test2 -test3')
        self.assertEqual(self.ts3.construct_command('testcommand', keys={'key1': b'test'}), "testcommand key1=b'test'")

        self.assertEqual(self.ts3.construct_command('testcommand', keys={'key1': b'test', 'key2': 'test'}), "testcommand key1=b'test' key2=b'test'")


        self.assertEqual(self.ts3.construct_command('testcommand', keys={'key1': b'test', 'key2': [1, 2, 3]}), "testcommand key1=b'test' key2=1|key2=2|key2=3")


        self.assertEqual(self.ts3.construct_command('testcommand', keys={'key1': b'test', 'key2': 'test'}, opts=['test']), "testcommand key2=b'test' key1=b'test' -test")
    
    def testParseData(self):
        # some response examples taken from http://media.teamspeak.com/ts3_literature/TeamSpeak%203%20Server%20Query%20Manual.pdf

        data = b'timestamp=1259356318 level=4 channel=Query msg=query\sfrom\s87.163.52.195:9\sissued:\slogview\slimitcount=30|timestamp=1259356148'
        parsed = [{'msg': 'query from 87.163.52.195:9 issued: logview limitcount=30', 'timestamp': '1259356318', 'channel': 'Query', 'level': '4'}, {'timestamp': '1259356148'}]

        self.assertEqual(self.ts3.parse_data(data), parsed)

        data = b'cid=2 cldbid=9 cgid=9|cid=2 cldbid=24 cgid=9|cid=2 cldbid=47 cgid=9'
        parsed = [{'cgid': '9', 'cldbid': '9', 'cid': '2'}, {'cgid': '9', 'cldbid': '24', 'cid': '2'}, {'cgid': '9', 'cldbid': '47', 'cid': '2'}]

        self.assertEqual(self.ts3.parse_data(data), parsed)

        data = b'client_unique_identifier=P5H2hrN6+gpQI4n\/dXp3p17vtY0= client_nickname=Rabe85 client_version=3.0.0-alpha24\s[Build:\s8785]\s(UI:\s8785)'
        parsed = {'client_unique_identifier': 'P5H2hrN6+gpQI4n/dXp3p17vtY0=', 'client_version': '3.0.0-alpha24 [Build: 8785] (UI: 8785)', 'client_nickname': 'Rabe85'}

        self.assertEqual(self.ts3.parse_data(data), parsed)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TS3ProtoTest))
    return suite

if __name__ == '__main__':
    unittest.main()
