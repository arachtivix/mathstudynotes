#! /usr/bin/mixguile \
-e main -s
!#

(define (listify-mem s e)
  (cond ((< e s) `())
	(else (cons (mix-cell s) (listify-mem (+ s 1) e)))))

(define (validate-memory expected starting)
  (cond ((= starting 4000) #t)
	((not (= (list-ref expected 0) (mix-cell starting)))
	 (display "failed at: ")
	 (display starting)
	 (display " expecting ")
	 (display (list-ref expected 0))
	 (display " found ")
	 (display (mix-cell starting))
	 (display "\n")
	 #f)
	(else (validate-memory (cdr expected) (+ starting 1)))))

(define main
  (lambda (args)
    (mix-load "aocp_v1_ch1.3.1_p21")
    (mix-sreg "I4" 123)
    (define before-mem (listify-mem 0 3999))
    (mix-run)
    (if (validate-memory before-mem 0)
	(display "memory is correct\n")
	(display "memory is incorrect\n"))
    (cond ((= (mix-reg "J") 123)
	   (display "jump register corrrect: ")
	   (display (mix-reg "J")))
	  (else
	   (display "jump register incorrect: ")
	   (display (mix-reg) "J"))
    (mix-pall)))
