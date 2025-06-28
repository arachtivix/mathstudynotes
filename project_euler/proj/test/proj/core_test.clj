(ns proj.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [proj.core :refer [solve-problem problems-data]]))

(deftest problems-data-test
  (testing "Problems data is loaded correctly"
    (is (map? problems-data))
    (is (vector? (:problems problems-data)))
    (is (every? number? (:problems problems-data)))))

;; removing slow test for now -- need to make profiles and run ones like these only remotely
;; TODO: ask Q to add test profile and add github worflow to run tests like these on push
;; (deftest solve-problem-test
;;   (testing "Solving non-existent problem"
;;     (is (= "Problem 0 not implemented yet"
;;            (solve-problem 0))))

;;   (testing "Solving existing problem"
;;     (let [first-problem (first (:problems problems-data))]
;;       (is (not= (str "Problem " first-problem " not implemented yet")
;;                 (solve-problem first-problem))))))