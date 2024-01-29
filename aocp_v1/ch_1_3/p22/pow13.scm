#! /usr/bin/mixguile \
-e main -s
!#

(define (ct-nonzero-lines s e)
  (cond ((> s e) 0)
	(define subct (ct-nonzero-lines (+ 1 s) e))
	((= (mix-cell s) 0) subct)
	(else (+ 1 subct))))

(define main
  (lambda (args)
    (mix-compile "pow13")
    (mix-load "pow13")
    (display "program instruction count: ")
    (display (ct-nonzero-lines 0 3999))
    (display "\n")
    (mix-smem 2000 3)
    (mix-run)
    (mix-pall)))
