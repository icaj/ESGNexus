package com.esgnexus.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "configuracoes")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ConfiguracaoSistema {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "chave", nullable = false, unique = true)
    private String chave;

    @Column(name = "valor", nullable = false)
    private String valor;
}
