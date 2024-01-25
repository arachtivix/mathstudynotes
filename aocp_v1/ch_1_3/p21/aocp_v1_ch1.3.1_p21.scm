#! /usr/bin/mixguile \
-e main -s
!#

(define (ct s e) (if (> e s) (cons e (ct s (- e 1))) `(,s)))

(define (listify-mem s e)
  (define idxs (ct s e))
  (map mix-cell idxs))

(define (validate-memory expected starting)
  (cond ((= starting 4000) #t)
	((not (= (list-ref expected 0) (mix-cell starting)))
	 (display "failed at: ")
	 (display starting)
	 (display " expecting ")
	 (display (list-ref expected 0))
	 (display " found ")
	 (display (mix-cell starting))
	 #f)
	(else (validate-memory (cdr expected) (+ starting 1)))))

(define main
  (lambda (args)
    (mix-load "aocp_v1_ch1.3.1_p21")
    (mix-sreg "I4" 123)
    (define before-mem (listify-mem 0 3999))
    ;(mix-run)
    ;(mix-set-cell! 10 101)
    (if (validate-memory before-mem 0)
	(display "success\n")
	(display "failure\n"))
    (mix-pall)))
