"""
Validadores de CPF e telefone.
"""
from validate_docbr import CPF
import re


cpf_validator = CPF()


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo dos dígitos verificadores.
    
    Args:
        cpf: CPF com ou sem formatação
        
    Returns:
        True se válido, False caso contrário
    """
    return cpf_validator.validate(cpf)


def normalizar_cpf(cpf: str) -> str:
    """
    Remove formatação do CPF.
    
    Args:
        cpf: CPF formatado
        
    Returns:
        CPF apenas com números
    """
    return re.sub(r'\D', '', cpf)


def validar_telefone_e164(telefone: str) -> bool:
    """
    Valida se telefone está no formato E.164.
    
    Args:
        telefone: Telefone a validar
        
    Returns:
        True se válido
    """
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, telefone))


def normalizar_telefone(telefone: str) -> str:
    """
    Normaliza telefone para formato E.164.
    
    Args:
        telefone: Telefone em qualquer formato
        
    Returns:
        Telefone no formato E.164
        
    Raises:
        ValueError: Se não conseguir normalizar
    """
    # Remove tudo que não é número
    apenas_numeros = re.sub(r'\D', '', telefone)
    
    # Se começa com 0, remove
    if apenas_numeros.startswith('0'):
        apenas_numeros = apenas_numeros[1:]
    
    # Se não começa com código do país, adiciona +55 (Brasil)
    if not telefone.startswith('+'):
        if len(apenas_numeros) == 11:  # DDD + 9 dígitos
            return f"+55{apenas_numeros}"
        elif len(apenas_numeros) == 10:  # DDD + 8 dígitos
            return f"+55{apenas_numeros}"
    
    # Se já tem +, valida
    if validar_telefone_e164(telefone):
        return telefone
    
    raise ValueError(f"Não foi possível normalizar o telefone: {telefone}")
