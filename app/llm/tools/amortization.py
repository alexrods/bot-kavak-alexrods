import pandas as pd
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_table(inputs: dict):
    """
    Calculates the amortization schedule for a given loan based on inputs.

    Args:
        inputs (dict): A dictionary containing the following keys:
            - price (float): The total value of the car.
            - down_payment (float): The initial down payment.
            - term (int): The term of the loan in years.

    Returns:
        tuple: A pandas DataFrame containing the amortization schedule and the monthly payment without VAT, 
               or (None, None) if an error occurs.

    # To DO: Create PDF and send to user. 
    """
    logger.info("Starting amortization calculation")
    try:
        valor = inputs['price']
        enganche = inputs['down_payment']
        plazo = inputs['term'] * 12
        tasa_anual = 0.1
        iva = 0.16

        saldo = valor - enganche
        tasa_interes_mensual = tasa_anual / 12
        cuota_mensual_sin_iva = saldo * (tasa_interes_mensual / (1 - (1 + tasa_interes_mensual) ** -plazo))
        saldo_inicial = saldo

        cuotas = []
        for i in range(1, plazo + 1):
            # Monthly interest
            intereses = saldo_inicial * tasa_interes_mensual
            
            # VAT on interest
            iva_intereses = intereses * iva
            
            # Amortization (portion of the payment that goes towards reducing the principal)
            amortizacion = cuota_mensual_sin_iva - intereses
            
            # Final balance after the payment
            saldo_final = saldo_inicial - amortizacion
            
            # Add the data to the list of payments
            cuotas.append({
                "Month": i,
                "Balance": round(saldo_inicial, 2),
                "Monthly Payment": round(cuota_mensual_sin_iva, 2),
                "Interest": round(intereses, 2),
                "VAT on Interest": round(iva_intereses, 2),
                "Principal": round(amortizacion, 2),
                "Final Balance": abs(round(saldo_final, 2))
            })
            
            # Update the initial balance for the next month
            saldo_inicial = saldo_final
        
        # Convert the list of payments to a DataFrame for readability
        df_amortizacion = pd.DataFrame(cuotas)
        df_amortizacion.to_csv("outputs/amortization.csv")
        logger.info("Amortization schedule calculation completed successfully")
        
        return df_amortizacion, round(cuota_mensual_sin_iva, 2)
    
    except Exception as e:
        logger.error(f"An error occurred during calculations: {e}")
        return None, None
