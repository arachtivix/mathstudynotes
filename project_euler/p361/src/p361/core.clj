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
