(ns proj.p51.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p51.core :refer [all-n-digit-primes all-n-digit-masks
                                   numbers-under-mask-all-same?
                                   num-to-masked get-valid-masked-values
                                   multi-assoc get-answer-for-num-digits]]))

(deftest test-all-n-digit-primes
  (testing "all-n-digit-primes"
    (is (= [2 3 5 7] (all-n-digit-primes 1)))
    (is (= [11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97] (all-n-digit-primes 2)))))

(deftest test-all-n-digit-masks
  (testing "all-n-digit-masks"
    (is (= ["X" "O"] (all-n-digit-masks 1)))
    (is (= ["XX" "XO" "OX" "OO"] (all-n-digit-masks 2))
    (is (= ["XXX" "XXO" "XOX" "XOO" "OXX" "OXO" "OOX" "OOO"] (all-n-digit-masks 3))))))

(deftest test-numbers-under-mask-all-same?
  (testing "number-under-mask-all-same?"
    (is (= true (numbers-under-mask-all-same? 1 "X")))
    (is (= true (numbers-under-mask-all-same? 1223 "OXXO")))
    (is (= false (numbers-under-mask-all-same? 1223 "XOOX")))
    (is (= true (numbers-under-mask-all-same? 1223 "XOOO")))
    (is (= true (numbers-under-mask-all-same? 1111 "XXXX")))
    (is (= false (numbers-under-mask-all-same? 1223 "XXXX")))))

(deftest test-num-to-masked
  (testing "num-to-masked"
    (is (= "X" (num-to-masked 1 "X")))
    (is (= "1" (num-to-masked 1 "O")))
    (is (= "1X" (num-to-masked 12 "OX")))
    (is (= "X2" (num-to-masked 12 "XO")))
    (is (= "12" (num-to-masked 12 "OO")))))

(deftest test-get-valid-masked-values
  (testing "get-valid-masked-values"
    (is (= ["1X3"] (get-valid-masked-values 123 ["OXO"])))
    (is (= [] (get-valid-masked-values 123 ["OXX"])))
    (is (= [] (get-valid-masked-values 121 ["XXO"])))
    (is (= ["1X1X" "X2X2"] (get-valid-masked-values 1212 ["OXOX" "XOXO"])))
    (is (= ["11XX" "1X1X"] (get-valid-masked-values 1111 ["OOXX" "OXOX"])))
    (is (= [] (get-valid-masked-values 1234 ["XXXX"])))))

(deftest test-multi-assoc
  (testing "multi-assoc"
    (is (= {2 [1] 3 [1]} (multi-assoc [2 3] {} 1)))
    (is (= {2 [1] 3 [1] 4 [3]} (multi-assoc [2 3] {4 [3]} 1)))
    (is (= {2 [1 3] 3 [1]} (multi-assoc [2 3] {2 [3]} 1)))))

(deftest test-get-answer-for-num-digits
  (testing "get-answer-for-num-digits"
    ;; examples from problem statement
    (is (= 13 (last (get-answer-for-num-digits 2 6))))
    (is (= 56003 (last (get-answer-for-num-digits 5 7))))))