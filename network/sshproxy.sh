#!/usr/bin/expect
set timeout 60
spawn /usr/bin/ssh -D 8118 -g exaos@insomnia247.nl
expect {
"password:" {
send "fuckthegfw\r"
}
}
interact {
timeout 60 { send " "}
}

