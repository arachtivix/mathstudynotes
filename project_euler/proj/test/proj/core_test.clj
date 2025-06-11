(ns proj.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer :all]
            [proj.core :refer :all]))

(deftest problem-imports-test
  (testing "Testing that problem namespaces are properly imported"
    (is (fn? solve-problem))
    (is (string? (solve-problem 999)))))
