(ns proj.p204.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p204.core :refer :all]))

(deftest remove-factors-test
  (testing "Testing remove factors"
    (is (= 13 (remove-factors 26 [2])))
    (is (= 26 (remove-factors 26 [5])))
    (is (= 26 (remove-factors 26 [])))
    (is (= 1 (remove-factors 27 [2 3])))
    (is (= 25 (remove-factors 100 [2 3])))))

(deftest simple-generalized-hamming-numbers-impl-seq-test
  (testing "Testing simple-generalized-hamming-numbers-impl-seq"
    (is (= '(1 2 3 4 5 6 8 9 10 12 15)
           (take 11 (simple-generalized-hamming-numbers-impl-seq 5))))
    (is (= '(1 2 3 4 5 6 7 8 9 10 12 14 15 16 18 20)
           (take 16 (simple-generalized-hamming-numbers-impl-seq 7))))))

(deftest brute-force-count-test
  (testing "Testing brute-force-count"
    (is (= 11 (brute-force-count 5 15)))
    (is (= 4 (brute-force-count 5 4)))
    (is (= 17 (brute-force-count 7 23)))))