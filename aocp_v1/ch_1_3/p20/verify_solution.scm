#! /usr/bin/mixguile \
-e main -s
!#

(define (ver loc val) (= (mix-cell loc) val))

(define disp-check
  (lambda (loc)
    (if (ver loc 133)
        (display ":) Success\n")
        (display ":( Failure\n"))))

(define main
  (lambda (args)
    (mix-load "aocp_v1_ch1.3.1_p20")
    (mix-sreg "I4" 123)
    (mix-run)
    (disp-check 3)
    (mix-pall)))