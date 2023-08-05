MEMT/Alignment/match.sh sys1 sys2 sys3 > dev.matched
MEMT/scripts/server.sh --lm.file corpora_train.lm.final.arpa.hi --port 2000
MEMT/scripts/zmert/run.rb . 2000  english 
MEMT/scripts/simple_decode.rb 2000 decoder_config dev.matched output
