/**
 * @author: Kai Kang
 *
 **/

#include <iostream>
#include <vector>
#include <eigen3/Eigen/Dense>
#include <math.h>

using namespace std;
using namespace Eigen;

#define ROW 3
#define COL 3

/**
 * Column-oriented Cholesky
 */
MatrixXd &cholesky(MatrixXd &m) {
  if (m.cols() == 0) {
    return m;
  }
  m(0, 0) = sqrt(m(0, 0)); // should not be zero
  MatrixXd r(1, m.cols()-1);
  for (int i = 1; i < m.cols(); i++) {
    float new_val = m(0, i) / m(0, 0);
    m(0, i) = new_val;
    m(i, 0) = new_val;
    r(0, i-1) = new_val;
  }
  MatrixXd to_subtract = r.transpose()*r;
  MatrixXd sub(m.rows()-1, m.cols()-1);
  for (int i = 1; i < m.rows(); i++) {
    for (int j = 1; j < m.cols(); j++) {
      sub(i-1, j-1) = m(i, j);
    }
  }
  sub -= to_subtract;
  // sub is now the Schur complement: M/A = D - CA^-1B
  cholesky(sub);
  for (int i = 1; i < m.rows(); i++) {
    for (int j = 1; j < m.cols(); j++) {
      m(i, j) = sub(i-1, j-1);
    }
  }
  return m;
}

int main() {
  cout << "Hello, Cholesky!" << endl;
  MatrixXd m(ROW, COL);
  float input[ROW*COL] = {4, 12, -16, 12, 37, -43, -16, -43, 98};
  for (int i = 0; i < ROW*COL; i++) {
    m(i/COL, i%COL) = input[i];
  }
  cout << m << endl;
  cholesky(m);
  cout << "cholesky factorization is\n" << m << endl;
  return 0;
}
