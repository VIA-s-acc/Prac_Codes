from .Poly import Polynom as Poly
class Prettier:
    """
    Class for pretty printing polynomials.
    
    - `pretty_polynom(Poly)`: Pretty print the polynomial
    """

    def pretty_polynom(Poly):
        """
        Pretty print the polynomial.

        Args:
            Poly: Polynomial

        Returns:
            String: Pretty polynomial
        """
        coeffs = Poly.get_coeffs()
        Poly_str = str(Poly)
        a = '\n\033[1m\033[95m' + '---Polynom---\n' +'\033[96m' + Poly_str +'\n'
        a += f'Coeffs {coeffs}\n' + '\033[0m'
        s = ''
        s += '\033[93m|\033[0m'
        max = 0
        for c in coeffs[::-1]:
            if len(str(c))+3 > max:
                max = len(str(c))+3
        i = 0
        for c in coeffs[::-1]:
            s += '\033[93m' + f' {f'A_{coeffs.index(c)}':>{max}} |'+ '\033[0m'
            i += len(' {:>{max}} |'.format(c, max = max))
        s += '\n'
        s += '\033[1m\033[92m' + '-'*(i+1)  + '\033[0m'
        s += '\033[93m'+'\n|'+'\033[0m'    
        for c in coeffs[::]:
            s += '\033[93m' + ' {:>{max}} |'.format(c, max = max) +'\033[0m'      
        s += '\n'
        s +=  '\033[1m\033[92m' +'-'*(i+1) + '\033[0m'
        a += '\033[1m\033[92m' + '-'*(i+1) + '\n' + '\033[0m'
        a += s
        a += '\n\033[1m\033[95m' + '---Polynom---\n' + '\033[0m'  
        a += '\033[1m\033[92m'  + '\033[0m'

        return a


