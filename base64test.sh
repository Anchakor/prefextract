#!/bin/sh
function testit {
    echo "Testing on:"
    echo $TSTR
    XTSTR=`php -r "echo strtr(base64_encode('$TSTR'), '+/', '-_');" 2> /dev/null`
    echo $XTSTR
    php -r "echo base64_decode(strtr('$XTSTR', '-_', '+/'));" 2> /dev/null
    echo
    export XTSTR=`python2 <<END
import os, base64
print(base64.urlsafe_b64encode(os.environ['TSTR']))
END`
    echo $XTSTR
    python2 <<END
import os, base64
print(base64.urlsafe_b64decode(os.environ['XTSTR']))
END
}

export TSTR='asděščřžýáíé-=[];\,./<>?:"|{}_+'
testit
export TSTR='sděščřžýáíé-=[];\,./<>?:"|{}_+'
testit

