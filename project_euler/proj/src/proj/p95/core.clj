(ns p95.core
  (:require [proj.shared :as shr]))

(def src-to-dest
  (reduce
   (fn [res n]
     (assoc res n (reduce + (shr/get-factors n))))
   {}
   (range 1 100)))
