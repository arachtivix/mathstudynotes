#! /usr/bin/mixguile \
-e main -s
!#

(define main
  (lambda (args)
    ;; load the file provided as a command line argument
    (mix-load "aocp_v1_ch1.3.1_p16_2")
    ;; execute it
    (mix-run)
    ;; get some memory locations
    (mix-pmem "0-7")
    (mix-pmem "999-1002")
    (mix-pmem "2999-3009")
    ;; print the contents of registers
    (mix-pall)))