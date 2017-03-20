/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package c3ucb;
import Jama.Matrix;
/**
 *
 * @author wudi
 */
public class Parameters {
    protected Matrix theta; //column vector [n][1]
    protected double beta;
    protected Matrix V; // matrix, shape = [d][d] 
    protected Matrix X; //matrix, shape = [increasing][d]
    protected Matrix Y; //column vector [increasing][1]
    
    public Parameters(int d, double initial_beta, double lamb){
        this.theta = new Matrix(d,1);
        this.V = Matrix.identity(d,d);
        this.X = new Matrix(1,d);
        this.Y = new Matrix(1,1);
        this.beta = initial_beta;
    }
}
