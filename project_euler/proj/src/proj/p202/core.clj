
(ns proj.p202.core
  (:gen-class))

;; Problem 202: Laserbeam
;; Created on 2025-06-23

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn is-named-vertex? [[horiz vert]]
  (and (>= vert 0) (= (mod (abs horiz) 2) (mod (abs vert) 2)) (<= (abs horiz) (abs vert))))

(defn -main []
  (println "Solution to Problem 202:")
  (println (solve)))
