package com.esgnexus.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;

public class CertificacaoDtos {
    public record CertificacaoRequest(
            @NotNull Long fornecedorId,
            @NotBlank String nome,
            String orgaoEmissor,
            LocalDate dataEmissao,
            LocalDate dataValidade,
            String status,
            String urlArquivo
    ) {}

    public record CertificacaoResponse(
            Long id,
            Long fornecedorId,
            String fornecedorNome,
            String nome,
            String orgaoEmissor,
            LocalDate dataEmissao,
            LocalDate dataValidade,
            String status,
            String urlArquivo
    ) {}
}
