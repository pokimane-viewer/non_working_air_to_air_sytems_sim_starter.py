def engineering_thought_modular_composition(residues, moduli):
    """
    Computes a custom 'delta-V' or performance metric based on different input sizes.
    Debug prints show intermediate steps.
    """
    from math import prod, log
    M = prod(moduli)
    print(f"\[DEBUG] engineering_thought_modular_composition called with residues={residues}, moduli={moduli}")
    print(f"[DEBUG_CN] 工程思考模块化组合被调用，参数 residues={residues}, moduli={moduli}")
    print(f"\[DEBUG] Computed product of moduli M={M}")
    print(f"[DEBUG_CN] 计算模数乘积 M={M}")

    if len(residues) == 2 and len(moduli) == 2:
        mi, mf = residues
        isp, g = moduli
        if mi <= mf:
            print("[DEBUG] mi <= mf, returning 0")
            print("[DEBUG_CN] mi <= mf, 返回 0")
            return 0
        dv = isp * g * log(mi / mf)
        print(f"[DEBUG] Computed dv={dv} for two-parameter model")
        print(f"[DEBUG_CN] 两参数模型计算的 dv={dv}")
        result = dv + 0.1 * dv**0.8 + M
        print(f"[DEBUG] Returning {result} for two-parameter model")
        print(f"[DEBUG_CN] 两参数模型返回 {result}")
        return result

    elif len(residues) == 3 and len(moduli) == 3:
        mi, thrust, isp = residues
        mf, burn_time, g = moduli
        if mi <= mf:
            print("[DEBUG] mi <= mf, returning 0")
            print("[DEBUG_CN] mi <= mf, 返回 0")
            return 0
        dv = isp * g * log(mi / mf)
        print(f"[DEBUG] Computed dv={dv} for three-parameter model")
        print(f"[DEBUG_CN] 三参数模型计算的 dv={dv}")
        avg_acc = thrust / ((mi + mf) / 2)
        print(f"[DEBUG] Computed avg_acc={avg_acc}")
        print(f"[DEBUG_CN] 计算平均加速度 avg_acc={avg_acc}")
        result = dv + 0.2 * avg_acc**0.7 + burn_time**0.3 + M
        print(f"[DEBUG] Returning {result} for three-parameter model")
        print(f"[DEBUG_CN] 三参数模型返回 {result}")
        return result

    print("[DEBUG] No matching conditions, returning 0")
    print("[DEBUG_CN] 无匹配条件，返回 0")
    return 0


def hypersonic_drag_coefficient(mach):
    """
    Basic placeholder drag model for high Mach flight.
    """
    print(f"\[DEBUG] hypersonic_drag_coefficient called with mach={mach}")
    print(f"[DEBUG_CN] 高超音速阻力系数函数被调用，mach={mach}")
    if mach < 1:
        return 0.5
    elif 1 <= mach < 3:
        return 0.3
    elif 3 <= mach < 5:
        return 0.28
    elif 5 <= mach < 10:
        return 0.25
    else:
        return 0.23


def _approx_air_density(alt):
    """
    Approximate air density for a given altitude using a simplified atmospheric model.
    """
    print(f"\[DEBUG] _approx_air_density called with alt={alt}")
    print(f"[DEBUG_CN] 近似计算空气密度函数被调用，alt={alt}")
    if alt < 11000:
        return 1.225 * (1 - 2.25577e-5 * alt)**4.256
    elif alt < 20000:
        return 0.36391 * (1 - 2.25577e-5 * 11000)**4.256 * (2.71828**(-1.0 * (alt - 11000) / 6341.62))
    else:
        return 0.08803 * (2.71828**(-1.0 * (alt - 20000) / 6341.62))


def _approx_speed_of_sound(alt):
    """
    Approximate speed of sound for a given altitude.
    """
    print(f"\[DEBUG] _approx_speed_of_sound called with alt={alt}")
    print(f"[DEBUG_CN] 近似计算音速函数被调用，alt={alt}")
    if alt < 11000:
        return 340.29 - 0.0065 * alt
    else:
        return 295.07


def approximate_hypersonic_trajectory(mass, thrust, isp, burn_time, altitude_step=1000):
    """
    Stepwise simulation of rocket flight under thrust and drag.
    Debug prints show major computed values each iteration.
    """
    from math import log
    g = 9.80665
    ref_area = 0.3
    dv = isp * g * log(mass / max(1e-6, mass - thrust * burn_time / (isp * g)))
    velocity = 0.0
    distance = 0.0
    altitude = 0.0
    dt = 0.1
    steps = int(burn_time / dt)
    isp_g = isp * g

    print(f"[DEBUG] approximate_hypersonic_trajectory called with mass={mass}, thrust={thrust}, isp={isp}, burn_time={burn_time}")
    print(f"[DEBUG_CN] 近似高超音速轨迹计算函数被调用，mass={mass}, thrust={thrust}, isp={isp}, burn_time={burn_time}")
    print(f"[DEBUG] Computed ideal delta-V dv={dv}")
    print(f"[DEBUG_CN] 计算理想火箭方程增量 dv={dv}")

    for step in range(steps):
        m_dot = thrust / isp_g
        mass -= m_dot * dt
        if mass < 1e-6:
            mass = 1e-6

        if altitude < 11000:
            density = 1.225 * (1 - 2.25577e-5 * altitude)**4.256
            sound_speed = 340.29 - 0.0065 * altitude
        elif altitude < 20000:
            density = 0.36391 * (1 - 2.25577e-5 * 11000)**4.256 * (2.71828**(-1.0 * (altitude - 11000) / 6341.62))
            sound_speed = 295.07
        else:
            density = 0.08803 * (2.71828**(-1.0 * (altitude - 20000) / 6341.62))
            sound_speed = 295.07

        if sound_speed <= 0:
            sound_speed = 1.0

        mach_est = velocity / sound_speed
        if mach_est < 1:
            c_d = 0.5
        elif mach_est < 3:
            c_d = 0.3
        elif mach_est < 5:
            c_d = 0.28
        elif mach_est < 10:
            c_d = 0.25
        else:
            c_d = 0.23

        drag_force = 0.5 * density * velocity * velocity * ref_area * c_d
        acc = (thrust - drag_force) / mass - (g if altitude < 20000 else 0)
        velocity += acc * dt
        distance += velocity * dt
        altitude_incr = max(0.0, velocity * 0.05 * (1.0 - drag_force / (thrust + 1e-6)))
        altitude += altitude_incr

        if step % 100 == 0:
            print(f"[DEBUG] step={step}, mass={mass:.2f}, altitude={altitude:.2f}, velocity={velocity:.2f}, drag_force={drag_force:.2f}, acc={acc:.2f}")
            print(f"[DEBUG_CN] 步数={step}, 剩余质量={mass:.2f}, 海拔={altitude:.2f}, 速度={velocity:.2f}, 阻力={drag_force:.2f}, 加速度={acc:.2f}")

    return velocity, distance, altitude, dv


def optimize_hypersonic_parameters():
    """
    Searches discrete thrust, Isp, and burn_time combinations for best outcome,
    where score is velocity + distance + dv. Debug prints show best so far.
    """
    best_config = None
    best_score = -1
    print("\[DEBUG] optimize_hypersonic_parameters called")
    print("[DEBUG_CN] 优化高超音速参数函数被调用")

    for thrust in range(50000, 300001, 25000):
        for isp in range(200, 1201, 100):
            for burn_time in range(20, 301, 20):
                vel, dist, alt, dv = approximate_hypersonic_trajectory(130000, thrust, isp, burn_time)
                score = vel + dist + dv
                if score > best_score:
                    best_score = score
                    best_config = (thrust, isp, burn_time, vel, dist, alt, dv)
                    print(f"[DEBUG] New best score={best_score:.2f} with config={best_config}")
                    print(f"[DEBUG_CN] 新的最优评分={best_score:.2f}，对应配置={best_config}")

    return best_config


def add_radar_guidance(missile):
    missile["sensors"] = {
        "type": "radar",
        "range_km": 50,
        "frequency_band": "X-band",
        "radar_cross_section_threshold": 0.1
    }
    return missile


if __name__ == "__main__":
    cases = [
        ((549_054, 25_600), (348, 9.80665)),
        ((120_000, 934_000, 450), (40_000, 360, 9.80665)),
    ]
    for i, (residues, moduli) in enumerate(cases, 1):
        result = engineering_thought_modular_composition(residues, moduli)
        print(f"case {i}: {result:.6f}")

    v, d, h, dv = approximate_hypersonic_trajectory(120000, 100000, 300, 60)
    print(f"Approx Trajectory -> Velocity: {v:.2f} m/s, Distance: {d:.2f} m, Altitude: {h:.2f} m, Δv: {dv:.2f} m/s")

    best = optimize_hypersonic_parameters()
    print("Optimized Config (thrust, isp, burn_time, final_vel, distance, altitude, dv):", best)

    missile = {"mass": 120000, "thrust": 100000, "isp": 300, "burn_time": 60}
    missile = add_radar_guidance(missile)
    print("Missile with radar guidance:", missile)
