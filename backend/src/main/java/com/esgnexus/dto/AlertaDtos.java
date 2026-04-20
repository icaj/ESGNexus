package com.esgnexus.dto;

public class AlertaDtos {
    public record AlertaResponse(
            Long id,
            Long fornecedorId,
            String fornecedorNome,
            String tipoAlerta,
            String severidade,
            String titulo,
            String descricao,
            String status,
            String dataCriacao
    ) {}
}
