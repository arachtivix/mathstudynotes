#! /usr/bin/mixguile \
-e main -s
!#

(define main
  (lambda (args)
    (mix-compile "pow13")
    (mix-load "pow13")
    (mix-smem 2000 3)
    (mix-run)
    (mix-pall)))
