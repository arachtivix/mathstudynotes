(ns p361.core)

(defn f
  ([n]
   (f n 0))
  ([n c]
   (cond (= n 0) c
         (= n 1) (+ c 1)
         :else (let [r (mod n 2)
                     d (bigint (/ n 2))]
                 (if (= r 0)
                   (recur d c)
                   (recur d (+ 1 c)))))))

(def sample-f
  (map
   f
   (range 100)))


(defn has-x-consec
  ([n x]
   (if (< x 1) true
       (let [two (bigint 2)
             one (bigint 1)
             bi-n (bigint n)
             bi-x (bigint x)]
     (has-x-consec (bigint (/ bi-n two)) one bi-x (mod bi-n two)))))
  ([n consec-so-far tot prev]
   (cond (= consec-so-far tot) true
         (= n (bigint 0)) false
         :else (let [remainder (mod n (bigint 2))
                     new-n (bigint (/ n (bigint 2)))]
           (if (= remainder prev)
             (recur new-n (+ consec-so-far (bigint 1)) tot remainder)
             (recur new-n 1 tot remainder))))))





