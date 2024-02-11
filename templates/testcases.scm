#! /usr/bin/mixguile \
-e main -s
!#

(define (ct-nonzero-lines s e)
  (define subct (cond ((> s e) 0)
		       (else (ct-nonzero-lines (+ 1 s) e))))
  (cond ((or (> s e) (= (mix-cell s) 0)) subct)
	(else (+ 1 subct))))

(define program "solution")
(define main
  (lambda (args)
    (mix-compile program)
    (display "instruction count: ")
    (display (ct-nonzero-lines 0 3999))
    (display "\n")
    (mix-load program)
    (mix-run)
