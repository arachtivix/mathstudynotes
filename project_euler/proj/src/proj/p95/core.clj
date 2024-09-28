(ns p95.core
  (:require [proj.shared :as shr]))

(defn proper-factors
  ([n]
   (if (> n 1)
     (proper-factors n (- n 1) '())
     '()))
  ([n c r]
   (if (= c 1) (cons 1 r)
       (if (= 0 (mod n c))
         (recur n (- c 1) (cons c r))
         (recur n (- c 1) r)))))

(defn sum-proper-factors
  [n] (reduce + (proper-factors n)))

(defn try-amic
  ([n lim]
   (amic-chain n n #{n} (list n) lim))
  ([orig curr seen path lim]
   (let [nxt (sum-proper-factors curr)]
     (cond (> nxt lim) {:ans path :is-amic false}
           (< nxt 2) {:ans path :is-amic false}
           (and (= curr orig) (= nxt curr)) (list orig)
           (and (contains? seen nxt) (= nxt orig)) {:ans path :is-amic true}
           (contains? seen nxt) {:ans path :is-amic false}
           :else (recur orig nxt (conj seen curr) (cons curr path))))))


(defn work-it
  ([n]
   (work-it n #{} 0 '()) 1000000)
  ([n seen b-len best lim]
   
