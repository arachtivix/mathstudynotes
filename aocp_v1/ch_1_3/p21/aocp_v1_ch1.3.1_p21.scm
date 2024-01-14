#! /usr/bin/mixguile \
-e main -s
!#

(define main
  (lambda (args)
    (mix-load "aocp_v1_ch1.3.1_p21")
    (mix-sreg "I4" 123)
    (mix-run)
    (mix-pall)))