
(ns proj.p3.core
  (:gen-class))

(def q 600851475143)

(defn up-by-twos
  [start] (lazy-seq (cons start (up-by-twos (+ start 2)))))

(defn get-check-range
  [n]
  (conj
   (take-while #(<= (* % %) n) (up-by-twos 3))
   2))

(defn get-factors
  ([n] (get-factors n (get-check-range n)))
  ([n [first-factor & remain :as try-factors]]
   (cond (= 1 n)
         '()
         (= 0 (count try-factors))
         (list n)
         (= 0 (mod n first-factor))
         (let [nn (/ n first-factor)]
           (conj (get-factors nn try-factors) first-factor))
         :else (recur n remain))))

(defn solve []
  (print (get-factors 600851475143)))

(defn -main []
  (println "Solution to Problem 3:")
  (println (solve)))