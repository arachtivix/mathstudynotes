#! /usr/bin/mixguile \
-e main -s
!#

(define (traverse-cycle start-idx curr-idx input output)
  (define nxt (vector-ref input curr-idx))
  (cond ((= -1 (vector-ref output curr-idx))
	 (vector-set! output curr-idx start-idx)
	 (traverse-cycle start-idx nxt input output))))

(define (check idx input output)
  (define pre (vector-ref output idx))
  (traverse-cycle idx idx input output)
  (define post (vector-ref output idx))
  (define contrib (if (= pre post) 0 1))
  (+ contrib
     (if (< (+ 1 idx) (vector-length input))
	 (check (+ 1 idx) input output)
	 0)))

(define (count-cycles vec)
  (display vec)
  (define vlen (vector-length vec))
  (define cycle-start (make-vector vlen -1))
  (newline)
  (display vlen)
  (newline)
  (display cycle-start)
  (newline)
  (define cycles-count (check 0 vec cycle-start))
  (display cycle-start)
  (newline)
  (display cycles-count)
  (newline))

(define main
  (lambda (args)
    (display "counting cycles")
    (newline)
    (define input #(2 3 4 5 0 1 6))
    (count-cycles input)
    (newline)))
