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
    protected double lamb;
    protected double delta;
    protected double gama;
    protected double R;
    
    public Parameters(Setting s){
        this.theta = new Matrix(s.d,1);
        this.V = Matrix.identity(s.d,s.d);
        this.X = new Matrix(1,s.d);
        this.Y = new Matrix(1,1);
        this.beta = s.initial_beta;
        this.lamb = s.lamb;
        this.gama = s.gama;
        this.R = s.R;
        
    }
}
