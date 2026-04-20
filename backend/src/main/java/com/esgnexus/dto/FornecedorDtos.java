package com.esgnexus.dto;

import jakarta.validation.constraints.NotBlank;

public class FornecedorDtos {
    public record FornecedorRequest(
            @NotBlank String razaoSocial,
            String nomeFantasia,
            @NotBlank String cnpj,
            String email,
            String telefone,
            String nomeContato,
            String segmento,
            String categoria,
            String cidade,
            String estado,
            String pais,
            String nivelRisco,
            String status
    ) {}

    public record FornecedorResponse(
            Long id,
            String razaoSocial,
            String nomeFantasia,
            String cnpj,
            String email,
            String telefone,
            String nomeContato,
            String segmento,
            String categoria,
            String cidade,
            String estado,
            String pais,
            String nivelRisco,
            String status
    ) {}
}
