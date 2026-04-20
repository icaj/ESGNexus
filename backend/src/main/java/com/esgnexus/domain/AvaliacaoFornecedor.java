package com.esgnexus.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Table(name = "avaliacoes_fornecedor")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AvaliacaoFornecedor {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "fornecedor_id")
    private Fornecedor fornecedor;

    @Column(name = "data_avaliacao", nullable = false)
    private LocalDate dataAvaliacao;

    @Column(name = "nota_ambiental", nullable = false)
    private Double notaAmbiental;

    @Column(name = "nota_social", nullable = false)
    private Double notaSocial;

    @Column(name = "nota_governanca", nullable = false)
    private Double notaGovernanca;

    @Column(name = "nota_final", nullable = false)
    private Double notaFinal;

    @Column(name = "observacoes")
    private String observacoes;
}
