from arcus.exc import (
    AlreadyPaid,
    DuplicatedPayment,
    IncompleteAmount,
    InvalidAccountNumber,
    InvalidAmount,
    RecurrentPayments,
)

errors_dict = {
    RecurrentPayments: 'Esta cuenta tiene pagos domiciliados activos '
    'y no acepta este tipo de pago',
    DuplicatedPayment: 'Posible pago duplicado. Intenta en 1 hora.',
    IncompleteAmount: 'Este proveedor no acepta pagos parciales,'
    ' asegúrate de cubrir el monto en su totalidad',
    AlreadyPaid: 'El balance en esta cuenta ya ha sido cubierto',
    InvalidAccountNumber: 'Por favor, verifica el número de telefono '
    'e intenta de nuevo',
    InvalidAmount: 'El monto a pagar es inválido.',
}
