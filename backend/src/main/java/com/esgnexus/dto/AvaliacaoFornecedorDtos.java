package com.esgnexus.dto;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;

public class AvaliacaoFornecedorDtos {
    public record AvaliacaoRequest(
            @NotNull Long fornecedorId,
            @NotNull LocalDate dataAvaliacao,
            @NotNull @DecimalMin("0.0") @DecimalMax("100.0") Double notaAmbiental,
            @NotNull @DecimalMin("0.0") @DecimalMax("100.0") Double notaSocial,
            @NotNull @DecimalMin("0.0") @DecimalMax("100.0") Double notaGovernanca,
            String observacoes
    ) {}

    public record AvaliacaoResponse(
            Long id,
            Long fornecedorId,
            String fornecedorNome,
            LocalDate dataAvaliacao,
            Double notaAmbiental,
            Double notaSocial,
            Double notaGovernanca,
            Double notaFinal,
            String observacoes
    ) {}
}
