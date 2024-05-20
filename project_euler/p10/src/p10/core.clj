(ns p10.core)


(defn calc-next-range
  [p]
  (range (+ p 2) (+ 2 (* p p)) 2))

(defn seq-contains-no-divisor
  [[:as ls] n]
  (if (not (some #(= 0 (mod n %)) ls))
    n
    nil))

(defn primes
  [prev-primes]
  (let [rng (calc-next-range (apply max prev-primes))]
    (filter
     #(eval %)
     (pmap
      #(seq-contains-no-divisor prev-primes %) rng))))

(def long-seq-o-primes
  (let [p1 [2 3 5]
        p2 (concat p1 (primes p1))
        p3 (concat p2 (primes p2))
        p4 (concat p3 (primes p3))
        p5 (concat p4 (primes p4))]
    p5))

; takes a min or two -- probably way overshooting the number of primes
; needed in the sequence
(def answ (apply + (take-while #(<= % 2000000) long-seq-o-primes)))

(println "answ = " answ)

