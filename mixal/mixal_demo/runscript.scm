#! /usr/bin/mixguile \
-e main -s
!#

(define main
  (lambda (args)
    ;; load the file provided as a command line argument
    (mix-load (cadr args))
    ;; execute it
    (mix-run)
    ;; print the contents of registers
    (mix-pall)))