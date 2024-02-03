#! /usr/bin/mixguile \
-e main -s
!#

(define (ct-nonzero-lines s e)
  (define subct (cond ((> s e) 0)
		       (else (ct-nonzero-lines (+ 1 s) e))))
  (cond ((or (> s e) (= (mix-cell s) 0)) subct)
	(else (+ 1 subct))))

(define (pow p v)
  (if (= p 1)
      v
      (* v (pow (- p 1) v))))

(define alltrue
  (lambda (ls)
    (cond ((null? ls) #t)
	  ((car ls) (alltrue (cdr ls)))
	  (else #f))))

(define (xor a b) (not (= a b)))

(define (match-lists l1 l2)
  (define l1nil (= l1 '()))
  (define l2nil (= l2 '()))
  (define one (xor l1nil l2nil))
  (define zero (and l1nil l2nil))
  (cond ((zero) (display "equal") #t)
	((one) (display "size mismatch") #f)
	((= (car l1) (car l2)) (match-lists (cdr l1) (cdr l2)))
	(else #f)))

(define main
  (lambda (args)
    (mix-compile "pow13_loop")
    (define (runtest testval)
      (display "running test input ")
      (display testval)
      (display "\n")
      (display "program instruction count: ")
      (display (ct-nonzero-lines 0 3999))
      (display "\n")
      (mix-load "pow13_loop")
      (mix-smem 2000 testval)
      (mix-run)
      (define result (mix-reg "A"))
      (define expected (pow 13 testval))
      (display "expected: ")
      (display expected)
      (display "\n")
      (display "result: ")
      (display result)
      (display "\n")
      (display "Program time: ")
      (display (mix-prog-time))
      (display "\n")
      (= result expected))
    (define vals '(-4 -3 -2 -1 0 1 2 3 4))
    (define results (map runtest vals))
    (if (alltrue results)
	(display "success")
	(display "failure"))))
