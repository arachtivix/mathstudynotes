(ns proj.core
  #_{:clj-kondo/ignore [:unused-namespace]}
  (:require [clojure.math :as math]
            [clojure.edn :as edn]
            [clojure.java.io :as io]
            [proj.shared :as shared])
  (:gen-class))

(def problems-data
  (-> "proj/problems.edn"
      io/resource
      slurp
      edn/read-string))

(defn require-problem [n]
  (try
    (require (symbol (format "proj.p%d.core" n)))
    true
    (catch Exception _
      false)))

(defn get-problem-ns [n]
  (symbol (format "proj.p%d.core" n)))

(defn solve-problem
  "Solves the specified Project Euler problem"
  [problem-number]
  (if (some #{problem-number} (:problems problems-data))
    (do
      (require-problem problem-number)
      (let [problem-ns (get-problem-ns problem-number)
            solve-fn (resolve (symbol (str problem-ns "/solve")))]
        (if solve-fn
          (solve-fn)
          (str "Problem " problem-number " exists but solve function not found"))))
    (str "Problem " problem-number " not implemented yet")))

(defn -main
  "Main entry point - solves the specified problem or lists available problems"
  [& args]
  (if (empty? args)
    (let [problems (sort (:problems problems-data))]
      (println "Available problems:" (clojure.string/join ", " problems)))
    (let [problem-number (Integer/parseInt (first args))]
      (println "Solution to Problem" problem-number ":")
      (println (solve-problem problem-number)))))
