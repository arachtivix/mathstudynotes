:(ns proj.p16.core
  (:gen-class))

(defn n-to-pow
  [n p]
  (reduce
   (fn [r _]
     (* r n))
   1
   (range p)))

(def two-pow-thous
  (n-to-pow (bigint 2) (bigint 1000)))

(defn sum-base-10-digits
  ([n]
   (sum-base-10-digits n 0))
  ([n s]
   (cond (= n 0) s
         :else (recur (bigint (/ n 10)) (+ (mod n 10) s)))))

(defn solve []
  (sum-base-10-digits two-pow-thous))

(defn -main []
  (println "Solution to Problem 16:")
  (println (solve)))
