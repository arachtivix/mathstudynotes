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

