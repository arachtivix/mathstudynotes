(ns proj.p205.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p205.core :refer :all]))

(deftest assoc-or-compute-test
  (testing "Testing assoc-or-compute"
    (is (= {1 1} (assoc-or-compute {} + 1 1)))
    (is (= {1 2} (assoc-or-compute {1 1} + 1 1)))
    (is (= {1 2 3 4} (assoc-or-compute {1 1 3 4} + 1 1)))
    (is (= {1 0 2 3} (assoc-or-compute {1 1 2 3} + 1 -1)))))

(deftest seq-assoc-or-compute-test
  (testing "Testing seq-assoc-or-compute"
    (is (= {} (seq-assoc-or-compute {} + '() '())))
    (is (= {1 1} (seq-assoc-or-compute {} + '(1) '(1))))
    (is (= {1 1} (seq-assoc-or-compute {} + '(1) '(1 2))))
    (is (= {1 2} (seq-assoc-or-compute {1 1} + '(1) '(1))))
    (is (= {1 2} (seq-assoc-or-compute {1 1} + '(1 2) '(1))))
    (is (= {1 1 2 1} (seq-assoc-or-compute {2 1} + '(1) '(1))))
    (is (= {1 1 2 2} (seq-assoc-or-compute {2 1} + '(1 2) '(1 1))))
    (is (= {1 1 2 2} (seq-assoc-or-compute {2 1} + '(1 2 3) '(1 1))))))


(deftest combine-rolls-test
  (testing "Testing combine-rolls"
    (is (= {2 1, 3 1} (combine-rolls {1 1, 2 1} {1 1})))
    (is (= {2 1, 3 2, 4 1} (combine-rolls {1 1, 2 1} {1 1, 2 1})))
    (is (= {2 2, 3 11, 4 5} (combine-rolls {1 2, 2 1} {1 1, 2 5})))
    (is (= {2 1, 3 1, 4 1, 5 2, 6 1} (combine-rolls {1 1, 2 1} {1 1, 3 1, 4 1})))
    (is (= {42 1, 104 1, 22 1, 84 1} (combine-rolls {37 1, 17 1} {5 1, 67 1})))))