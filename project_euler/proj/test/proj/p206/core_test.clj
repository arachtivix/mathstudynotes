(ns proj.p206.core-test
  (:require [clojure.test :refer :all]
            [proj.p206.core :refer :all]))

(deftest dec-exp-int-test
  (testing "Testing decimal expansion of integers"
    (is (= '(1 0 0 0) (dec-exp-int 1000)))
    (is (= '(1 2 3 4) (dec-exp-int 1234)))
    (is (= '(0) (dec-exp-int 0)))))

(deftest matches-pattern-test
  (testing "Testing matches pattern"
    (is (= true (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4))))
    (is (= false (matches-pattern? '(1 :_ 2 :_) '(1 2 3 4))))
    (is (= false (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4 5))))))

(deftest matches-pattern-test
  (testing "Testing matches pattern with leading zeros"
    (is (= false (matches-pattern? '(:_ :_ 3 :_) '(4))))
    (is (= true (matches-pattern? '(:_ :_ 3 :_) '(3 4))))
    (is (= true (matches-pattern? '(:_ :_ 3 :_) '(1 3 4))))
    (is (= false (matches-pattern? '(:_ :_ 3 :_) '(1 5 5 3 2))))))

(deftest dec-exp-to-bigint-test
  (testing "Testing decimal expansion to bigint"
    (is (= 1234 (dec-exp-to-bigint '(1 2 3 4))))
    (is (= 0 (dec-exp-to-bigint '())))
    (is (= 999999999999999999999999999999 (dec-exp-to-bigint (take 30 (repeat 9)))))))

(deftest pat-min-test
  (testing "Testing pattern minimum value function"
    (is (= 1030 (patt-min '(1 :_ 3 :_))))
    (is (= 0 (patt-min '(:_ :_ :_ :_))))
    (is (= 1234 (patt-min '(1 2 3 4))))))

(deftest pat-max-test
  (testing "Testing pattern minimum value function"
    (is (= 1939 (patt-max '(1 :_ 3 :_))))
    (is (= 9999 (patt-max '(:_ :_ :_ :_))))
    (is (= 1234 (patt-max '(1 2 3 4))))))

(deftest brute-force-generalized-test
  (testing "Testing the brute force approach generalized"
    (is (= '(4) (brute-force-generalized '(1 :_))))
    (is (= '(12) (brute-force-generalized '(1 4 :_))))
    (is (= '(12) (brute-force-generalized '(1 4 :_))))
    (is (= '(123) (brute-force-generalized '(1 5 1 :_ :_))))
    (is (= '(123 124 125 126) (brute-force-generalized '(1 5 :_ :_ :_))))
    ;; made a spreadsheet and verified the following manually
    (is (= '(104 106 114 116 124 126 134 136) (brute-force-generalized '(1 :_ :_ :_ 6))))))

(deftest get-bases-matching-pattern-test
  (testing "Testing get-bases-matching-pattern -- data from table in writeup"
    (is (= '(2 8) (get-bases-matching-pattern (numbered-cyc-vals 1) '(4))))
    (is (= '(5) (get-bases-matching-pattern (numbered-cyc-vals 1) '(5))))
    (is (= '() (get-bases-matching-pattern (numbered-cyc-vals 1) '(8))))))

(deftest get-try-deltas-test
  (testing "Testing get-try-deltas"
    (is (= [2 [6 4]] (get-try-deltas 1 '(4))))
    (is (= [4 [2 8]] (get-try-deltas 1 '(6))))
    (is (= [0 [10]] (get-try-deltas 1 '(0))))
    (is (= [nil []] (get-try-deltas 1 '(7))))
    (is (= [3 [44 6]] (get-try-deltas 2 '(9))))))