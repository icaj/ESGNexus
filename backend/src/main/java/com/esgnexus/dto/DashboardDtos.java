package com.esgnexus.dto;

import java.util.List;

public class DashboardDtos {
    public record DashboardKpis(
            long totalFornecedores,
            long totalAvaliacoes,
            long totalCertificacoes,
            long alertasAbertos,
            double mediaScore
    ) {}

    public record ItemRanking(Long fornecedorId, String fornecedorNome, Double notaFinal) {}

    public record DashboardResponse(DashboardKpis indicadores, List<ItemRanking> topRanking) {}
}
