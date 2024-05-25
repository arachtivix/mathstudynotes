(ns p12.core)

; it seems these may have little to do with the solution, but I
; made a slightly handier way of getting a specific number of primes
; tonight
(defn next-prime
  ([start]
   (next-prime start '()))
  ([start [p & rp :as prev-primes]]
  (cond (nil? p) 2
        (= p 2) 3
        :else (first
               (filter
                #(not (some (fn [x] (= 0 (mod % x))) prev-primes))
                (iterate #(+ 2 %) start))))))

(defn n-primes
  [n]
  (cond (< n 1) '(2)
        (= n 2) '(3 2)
        :else (let [[gt :as prev-primes] (n-primes (- n 1))]
                (cons (next-prime (+ 2 gt) prev-primes) prev-primes))))

; get a list of prime factors in their frequencies
(defn factorize-partial
  ([n] (factorize-partial n '() '(2)))
  ([n [:as pfs] [top-test-factor :as primes]]
   (cond (= n 1)
         pfs
         (= 0 (mod n top-test-factor))
         (recur (/ n top-test-factor)
                (cons top-test-factor pfs)
                primes)
         :else
         (recur n
                pfs
                (cons (next-prime top-test-factor primes)
                      primes)))))

(defn relevant-freqs
  [n]
  (dissoc
   (frequencies
    (factorize-partial n))
   n))

(defn divisor-count
  [n]
  (apply *
         (reduce
          (fn [coll [k v]]
            (cons (+ 1 v) coll))
          '()
          (relevant-freqs n))))
