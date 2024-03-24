#! /usr/bin/mixguile \
-e main -s
!#

(load "scenarios.scm")

(define (ct-nonzero-lines s e)
  (define subct (cond ((> s e) 0)
		       (else (ct-nonzero-lines (+ 1 s) e))))
  (cond ((or (> s e) (= (mix-cell s) 0)) subct)
	(else (+ 1 subct))))

(define (run-test scenario program)
  (mix-compile program)
  (mix-load program)
  (define expected (scenario))
  (display "Starting test\n")
  (mix-run)
  (expected))

(define main
  (lambda (args)
    (run-test scen1 "solution")))
