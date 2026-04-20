package com.esgnexus.dto;

import jakarta.validation.constraints.NotBlank;

public class ConfiguracaoDtos {
    public record ConfiguracaoRequest(@NotBlank String chave, @NotBlank String valor) {}
    public record ConfiguracaoResponse(Long id, String chave, String valor) {}
}
